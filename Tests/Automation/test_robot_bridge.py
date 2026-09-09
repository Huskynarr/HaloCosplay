"""Robot telemetry must expire and a selftest must preserve live state."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "robot_bridge", ROOT / "Code/HelmetControl/robot_bridge.py")
bridge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bridge)


class RobotBridgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "hud_state.json"

    def test_invalid_values_and_unknown_only_packets_are_rejected(self):
        invalid = [b'{"robot_distance_m":2,\xff"robot_bearing":3}',
                   b'[]', b'{}', b'{"contacts":2}', b'not json']
        for key in ("robot_distance_m", "robot_bearing", "robot_battery"):
            for value in (-1, float("nan"), float("inf"), None, True, "2", []):
                invalid.append(json.dumps({key: value}))
        invalid.extend([json.dumps({"robot_bearing": 360}),
                        json.dumps({"robot_battery": 101}),
                        json.dumps({"robot_state": "attack"}),
                        json.dumps({"robot_state": []})])
        for packet in invalid:
            with self.subTest(packet=packet):
                self.assertIsNone(bridge.parse_datagram(packet))
        self.assertEqual(bridge.parse_datagram(
            '{"robot_distance_m":0,"robot_bearing":359.9,"robot_battery":100,"contacts":2}'),
            {"robot_distance_m": 0, "robot_bearing": 359.9, "robot_battery": 100})

    def test_snapshot_clears_missing_robot_fields_preserves_foreign(self):
        self.path.write_text(json.dumps({"ammo": 27, "temperature_c": 33,
                                        "robot_distance_m": 2, "robot_bearing": 90}))
        result = bridge.merge_into_state({"robot_state": "hold"}, self.path)
        self.assertEqual(result, {"ammo": 27, "temperature_c": 33,
                                  "robot_state": "hold"})
        self.assertEqual(json.loads(self.path.read_text()), result)
        before = self.path.read_bytes()
        with self.assertRaises(ValueError):
            bridge.merge_into_state({"robot_distance_m": float("nan")}, self.path)
        self.assertEqual(self.path.read_bytes(), before)

    def test_selftest_preserves_supplied_and_default_live_state(self):
        supplied = self.path
        default = Path(self.tmp.name) / "default.json"
        for path in (supplied, default):
            path.write_text('{"ammo":73,"robot_state":"follow"}\n')
        with mock.patch.object(bridge, "DEFAULT_STATE", str(default)), \
                contextlib.redirect_stdout(io.StringIO()):
            bridge.run_selftest(str(supplied))
            bridge.run_selftest()
        for path in (supplied, default):
            self.assertEqual(path.read_text(), '{"ammo":73,"robot_state":"follow"}\n')

    def test_invalid_packet_flood_does_not_keep_snapshot_alive(self):
        clock = [0.0]
        received = [0]
        fake_socket = mock.Mock()

        def receive(_size):
            received[0] += 1
            clock[0] += 1.0
            if received[0] == 1:
                return b'{"robot_distance_m":2}', ("127.0.0.1", 1111)
            if received[0] == 6:
                self.assertNotIn("robot_distance_m", json.loads(self.path.read_text()))
                raise KeyboardInterrupt
            # Neither garbage nor unknown-only JSON is a heartbeat.
            return (b'garbage' if received[0] % 2 else b'{"contacts":2}'), ("127.0.0.1", 1111)

        fake_socket.recvfrom.side_effect = receive
        with mock.patch.object(bridge.socket, "socket", return_value=fake_socket), \
                mock.patch.object(bridge.time, "monotonic", side_effect=lambda: clock[0]), \
                contextlib.redirect_stdout(io.StringIO()):
            bridge.run("127.0.0.1", 9009, self.path, stale_after=3.0)
        fake_socket.close.assert_called_once()

    def test_restart_clears_snapshot_before_first_datagram(self):
        self.path.write_text(json.dumps({"ammo": 19, "robot_state": "follow"}))
        fake_socket = mock.Mock()

        def receive(_size):
            self.assertEqual(json.loads(self.path.read_text()), {"ammo": 19})
            raise KeyboardInterrupt

        fake_socket.recvfrom.side_effect = receive
        with mock.patch.object(bridge.socket, "socket", return_value=fake_socket), \
                contextlib.redirect_stdout(io.StringIO()):
            bridge.run("127.0.0.1", 9009, self.path)

    def test_wrong_source_cannot_publish_telemetry(self):
        fake_socket = mock.Mock()
        fake_socket.recvfrom.side_effect = [
            (b'{"robot_distance_m":2}', ("192.0.2.2", 1111)), KeyboardInterrupt]
        with mock.patch.object(bridge.socket, "socket", return_value=fake_socket), \
                contextlib.redirect_stdout(io.StringIO()):
            bridge.run("127.0.0.1", 9009, self.path, source_ip="192.0.2.1")
        self.assertFalse(self.path.exists())

    def test_cli_default_listener_is_loopback(self):
        with mock.patch("sys.argv", ["robot_bridge.py"]), \
                mock.patch.object(bridge, "run") as run:
            bridge.main()
        self.assertEqual(run.call_args.args[0], "127.0.0.1")

    def test_expiry_must_be_positive_and_finite(self):
        for expiry in (0, -1, float("nan"), float("inf")):
            with self.subTest(expiry=expiry), self.assertRaises(ValueError):
                bridge.run("127.0.0.1", 9009, self.path, stale_after=expiry)

    def test_failed_publication_reports_failure_and_preserves_old_file(self):
        self.path.write_text('{"ammo":27}\n')
        with mock.patch.object(bridge, "atomic_write", return_value=False):
            with self.assertRaises(OSError):
                bridge.merge_into_state({"robot_distance_m": 2}, self.path)
        self.assertEqual(self.path.read_text(), '{"ammo":27}\n')

    def test_failed_expiry_is_retried_without_success_message(self):
        fake_socket = mock.Mock()
        fake_socket.recvfrom.side_effect = [
            (b'{"robot_distance_m":2}', ("127.0.0.1", 1111)),
            bridge.socket.timeout, KeyboardInterrupt]
        output = io.StringIO()
        with mock.patch.object(bridge.socket, "socket", return_value=fake_socket), \
                mock.patch.object(bridge.time, "monotonic", side_effect=[0, 4, 5]), \
                mock.patch.object(bridge, "clear_robot_state", side_effect=[True, False, False, False]) as clear, \
                contextlib.redirect_stdout(output):
            bridge.run("127.0.0.1", 9009, self.path)
        # Initial cleanup, two expiry attempts, final cleanup.
        self.assertEqual(clear.call_count, 4)
        self.assertNotIn("Snapshot entfernt", output.getvalue())

    def test_failed_publication_does_not_reset_expiry(self):
        fake_socket = mock.Mock()
        fake_socket.recvfrom.side_effect = [
            (b'{"robot_distance_m":2}', ("127.0.0.1", 1111)),
            (b'{"robot_distance_m":3}', ("127.0.0.1", 1111)),
            KeyboardInterrupt]
        # First snapshot at 0, another packet at 2 fails publication, at 4 the
        # original snapshot must expire. A success-only extra clock read fails.
        with mock.patch.object(bridge.socket, "socket", return_value=fake_socket), \
                mock.patch.object(bridge.time, "monotonic", side_effect=[0, 2, 4]), \
                mock.patch.object(bridge, "merge_into_state", side_effect=[{}, OSError]), \
                mock.patch.object(bridge, "clear_robot_state", return_value=True) as clear, \
                contextlib.redirect_stdout(io.StringIO()):
            bridge.run("127.0.0.1", 9009, self.path)
        self.assertEqual(clear.call_count, 3)  # startup, expiry, shutdown


if __name__ == "__main__":
    unittest.main()
