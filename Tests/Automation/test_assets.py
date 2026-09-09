import hashlib
import json
import os
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

from tools import suit_assets as assets

TRIANGLES = [((0,0,0),(0,1,0),(1,0,0)), ((0,0,0),(1,0,0),(0,0,1)),
             ((0,0,0),(0,0,1),(0,1,0)), ((1,0,0),(0,1,0),(0,0,1))]


def stl(triangles=TRIANGLES):
    rows = ['solid test']
    for tri in triangles:
        rows.extend(['facet normal 0 0 1', 'outer loop'])
        rows.extend('vertex '+' '.join(map(str,v)) for v in tri)
        rows.extend(['endloop','endfacet'])
    return ('\n'.join(rows+['endsolid test'])+'\n').encode('ascii')


class AssetTests(unittest.TestCase):
    def test_ascii_and_binary_units_and_edges(self):
        binary = b'solid binary'.ljust(80,b' ')+struct.pack('<I',4)
        for tri in TRIANGLES:
            binary += struct.pack('<12fH',0,0,1,*(v for vertex in tri for v in vertex),0)
        for data in (stl(),binary):
            report = assets.inspect_stl(data,10)
            self.assertEqual(report['size_mm'],[10,10,10])
            self.assertTrue(report['edge_checks_complete'])
        self.assertFalse(assets.inspect_stl(stl(TRIANGLES[:3]),1)['edge_checks_complete'])
        self.assertFalse(assets.inspect_stl(stl([*TRIANGLES[:3],tuple(reversed(TRIANGLES[3]))]),1)['edge_checks_complete'])

    def test_bad_meshes_and_implicit_units_rejected(self):
        for raw in (b'',b'solid empty\nendsolid empty',stl([((0,0,0),)*3]),stl().replace(b'vertex 0 0 0',b'vertex nan 0 0')):
            with self.assertRaises(ValueError): assets.inspect_stl(raw,1)
        for scale in (None,True,0,-1,float('nan')):
            with self.assertRaises(ValueError): assets.inspect_stl(stl(),scale)

    def test_manifest_files_hashes_and_missing_parts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            catalog=root/'catalog.json'
            catalog.write_text(json.dumps({'references':[{'id':'custom','parts':[{'id':'helmet','required_views':['front']},{'id':'undersuit','required_views':['front']}]}]}))
            with patch.object(assets,'CATALOG',catalog):
                data=assets.template('Test','custom')
                self.assertFalse(assets.evaluate(data,root)['file_checks_complete'])
                (root/'shape.scad').write_text('cube(10);')
                (root/'shape.stl').write_bytes(stl())
                (root/'pattern.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
                for row in data['parts']:
                    row.update(source_url='https://example.com/source',license_note='Original test fixture',reference_views=['front'])
                    name='shape.scad' if row['kind']=='mesh' else 'pattern.svg'
                    row.update(native_path=name,native_sha256=hashlib.sha256((root/name).read_bytes()).hexdigest())
                    if row['kind']=='mesh': row.update(mesh_path='shape.stl',mesh_sha256=hashlib.sha256(stl()).hexdigest(),unit_scale_mm=1)
                result=assets.evaluate(data,root)
                self.assertTrue(result['file_checks_complete'])
                self.assertFalse(result['authenticity_verified'])
                self.assertFalse(result['fabrication_approved'])
                data['parts'][0]['reference_views']=['arbitrary-note']
                self.assertFalse(assets.evaluate(data,root)['file_checks_complete'])
                data['parts'][0]['reference_views']=['front']
                (root/'shape.scad').write_text('cube(20);')
                self.assertFalse(assets.evaluate(data,root)['file_checks_complete'])
                data['parts'].append(data['parts'][0])
                with self.assertRaises(ValueError): assets.evaluate(data,root)

    def test_output_and_path_escape_protected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'part.stl').write_bytes(stl())
            with self.assertRaises(ValueError): assets.local_file(root,'../escape.stl')
            with self.assertRaises(ValueError): assets.local_file(root,str(root/'part.stl'))
            catalog=root/'catalog.json';catalog.write_text(json.dumps({'references':[{'id':'custom','parts':[{'id':'helmet','required_views':['front']}]}]}))
            with patch.object(assets,'CATALOG',catalog):
                manifest=root/'assets.json'
                self.assertEqual(assets.main(['--init',str(manifest),'--reference','custom']),0)
                self.assertEqual(assets.main(['--init',str(manifest),'--reference','custom']),2)
                before=manifest.read_bytes()
                self.assertEqual(assets.main(['--manifest',str(manifest),'--report',str(manifest)]),2)
                self.assertEqual(manifest.read_bytes(),before)
                alias=root/'report.json'
                os.link(manifest,alias)
                self.assertEqual(assets.main(['--manifest',str(manifest),'--report',str(alias)]),2)
                self.assertEqual(manifest.read_bytes(),before)


if __name__ == '__main__':
    unittest.main()
