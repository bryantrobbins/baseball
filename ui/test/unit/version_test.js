'use strict';

describe('app.version module', function() {
  beforeEach(module('app.version'));

  describe('version service', function() {
    it('should return current version', inject(function(version) {
      expect(version).toEqual('0.1');
    }));
  });
});
