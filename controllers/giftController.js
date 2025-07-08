const express = require("express");
const router = express.Router();
const matchController = require("../controllers/matchController");

router.get("/recommendations", matchController.getRecommendedProfiles);

module.exports = router;
