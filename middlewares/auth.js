module.exports = (req, res, next) => {
  const userId = req.headers['x-user-id'];
  if (!userId) return res.status(401).json({ error: 'User not authenticated' });
  req.userId = userId;
  next();
};
