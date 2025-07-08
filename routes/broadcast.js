const express = require("express");
const router = express.Router();
const broadcastController = require("../controllers/broadcastController");

router.post("/send", broadcastController.broadcastMessage);

module.exports = router;
