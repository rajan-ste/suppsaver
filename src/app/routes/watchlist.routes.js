module.exports = app => {
    const watchlist = require("../controllers/watchlist.controller.js");
    const { authenticateToken } = require("../middleware/authentication.js")
    const jwt = require('jsonwebtoken');
  
    var router = require("express").Router();

    // add a product to the watchlist
    router.post('/', authenticateToken, watchlist.create);

    // fetch watchlist products
    router.get('/', authenticateToken, watchlist.findById);
  
    app.use('/api/watchlist', router);
  };