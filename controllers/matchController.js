const User = require('../models/User');
const Interaction = require('../models/Interaction');

exports.getMatches = async (req, res) => {
  const userId = req.userId;
  const matches = await Interaction.find({ fromUser: userId, type: 'like' }).populate('toUser');
  const result = matches.map(i => i.toUser);
  res.json(result);
};

exports.likeUser = async (req, res) => {
  const { targetUserId } = req.body;

  const existing = await Interaction.findOne({ fromUser: req.userId, toUser: targetUserId });
  if (existing) return res.status(400).json({ error: 'Already interacted' });

  await Interaction.create({ fromUser: req.userId, toUser: targetUserId, type: 'like' });

  const isMutual = await Interaction.findOne({ fromUser: targetUserId, toUser: req.userId, type: 'like' });

  if (isMutual) {
    return res.json({ matched: true });
  }

  res.json({ matched: false });
};
