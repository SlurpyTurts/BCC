var express = require('express');
var router = express.Router();
//var database = require('../util/database')
//
// function buildBom(currentBomList, levelsLeft, parentBomId){
//   database.getConnection(function(err, connection){
//     connection.query('SELECT bom.parent, bom.child, bom.quantity, bom.referenceDesignator, part.description FROM bom INNER JOIN part ON bom.child = part.partNumber WHERE parent = ?',
//     [parentBomId], function(err, rows){
//        connection.release();
//        currentBomList.push(rows);
//     });
//   });
// }



/* GET BOM page. */
router.get('/', function(req, res, next) {
  res.render('bom', { });
});

module.exports = router;
