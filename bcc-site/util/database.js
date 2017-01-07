var mysql = require('mysql');

var pool = mysql.createPool({
  host     : 'localhost',
  user     : 'root',
  password : 'my-secret-password',
  database : 'bcc'
});

module.exports = pool;
