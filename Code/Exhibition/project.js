/* Presentation metadata only. No body measurements or control commands displayed. */
(function (root) {
  'use strict';
  function metadata(data) {
    if (!data || data.schema_version !== 1 || typeof data.profile !== 'string' || !data.profile.trim() || data.profile.length > 64) throw Error('Projektprofil mit Name und schema_version 1 erforderlich');
    const build = data.build;
    if (!build || typeof build !== 'object' || Array.isArray(build)) throw Error('Baukonfiguration fehlt');
    const values = ['armor_reference','material','operating_mode'].map(key => {
      const value = build[key];
      if (typeof value !== 'string' || !value.trim() || value.length > 80) throw Error('Projektangabe fehlt: ' + key);
      return value;
    });
    return {title: data.profile, summary: 'Referenz: ' + values[0] + ' | Material: ' + values[1] + ' | Betriebsart: ' + values[2] + '. Planangaben, kein Funktionsnachweis.'};
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {metadata};
  else root.HaloProject = {metadata};
})(typeof globalThis !== 'undefined' ? globalThis : this);
