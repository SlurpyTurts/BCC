var express = require('express');
//var connection = require('../util/database')
var router = express.Router();

/* GET Dealers page. */
router.get('/', function(req, res, next) {
  res.render('dealers', { });
});

module.exports = router;
