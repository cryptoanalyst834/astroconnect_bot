const mongoose = require('mongoose');

const interactionSchema = new mongoose.Schema({
  fromUser: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  toUser: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  type: {
    type: String,
    enum: ['like', 'block', 'report'],
    required: true
  },
  createdAt: { type: Date, default: Date.now }
});

interactionSchema.index({ fromUser: 1, toUser: 1 }, { unique: true });

module.exports = mongoose.model('Interaction', interactionSchema);
