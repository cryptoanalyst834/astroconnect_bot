const mongoose = require('mongoose');

const usageLimitSchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true, unique: true },
  dailyLikes: { type: Number, default: 0 },
  lastReset: { type: Date, default: Date.now }
});

module.exports = mongoose.model('UsageLimit', usageLimitSchema);
