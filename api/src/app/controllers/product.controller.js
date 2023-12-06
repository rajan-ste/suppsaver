const Product = require("../models/product.model.js");

// Create and Save new Products
exports.create = (req, res) => {
  // Validate request
  if (!req.body || !Array.isArray(req.body)) {
      return res.status(400).send({
          message: "Content can not be empty and should be an array!"
      });
  }

  // Iterate over each product in the array
  const creationPromises = req.body.map(productData => {
      return new Promise((resolve, reject) => {
          const product = new Product({
              productname: productData.productname,
              companyid: productData.companyid,
              price: productData.price,
              image: productData.image,
              link: productData.link,
          });

          Product.create(product, (err, data) => {
              if (err) {
                  reject(err);
              } else {
                  resolve(data);
              }
          });
      });
  });

  // Wait for all product creations to complete
  Promise.all(creationPromises)
      .then(results => res.send(results))
      .catch(err => {
          res.status(500).send({
              message: err.message || "Error occurred while creating the products."
          });
      });
};

// Retrieve all Products
exports.findAll = (req, res) => {

  Product.getAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Error occurred while retrieving products."
      });
    else res.send(data);
  });
};

// Find a single product with a id
exports.findByID = (req, res) => {

  Product.findById(req.params.productid, req.params.companyid, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Product with id ${req.params.productid} not found.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving product with id " + req.params.productid
        });
      }
    } else res.send(data);
  });
};

// Update a product identified by the id in the request
exports.update = (req, res) => {
  // Validate Request
  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }

  console.log(req.body);

  Product.updateById(
    req.params.productid, req.params.companyid,
    new Product(req.body),
    (err, data) => {
      if (err) {
        if (err.kind === "not_found") {
          res.status(404).send({
            message: `Product with id ${req.params.productid} not found.`
          });
        } else {
          res.status(500).send({
            message: "Error updating product with id " + req.params.productid
          });
        }
      } else res.send(data);
    }
  );
};

// Delete a product with the specified id in the request
exports.delete = (req, res) => {
  Product.remove(req.params.productid, req.params.companyid, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Product with id ${req.params.productid} not found.`
        });
      } else {
        res.status(500).send({
          message: "Could not delete product with id " + req.params.productid
        });
      }
    } else res.send({ message: `product was deleted successfully!` });
  });
};
