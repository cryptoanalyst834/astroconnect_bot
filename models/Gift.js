const mongoose = require('mongoose');

const giftSchema = new mongoose.Schema({
  sender: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  receiver: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  type: { type: String, enum: ['rose', 'heart', 'diamond'], required: true },
  message: { type: String, maxlength: 200 },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Gift', giftSchema);
