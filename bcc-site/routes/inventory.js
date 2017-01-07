var express = require('express');
//var connection = require('../util/database')
var router = express.Router();

/* GET BOM page. */
router.get('/', function(req, res, next) {
  res.render('inventory', { });
});

module.exports = router;
