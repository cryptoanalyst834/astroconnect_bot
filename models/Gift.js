const mongoose = require("mongoose");

const GiftSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  iconUrl: {
    type: String,
    required: true,
  },
  price: {
    type: Number, // в коинах/баллах
    required: true,
  },
});

module.exports = mongoose.model("Gift", GiftSchema);
