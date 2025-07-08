const express = require("express");
const router = express.Router();
const limitController = require("../controllers/limitController");

router.post("/increment", limitController.incrementUsage);
router.get("/:userId", limitController.getLimits);

module.exports = router;
