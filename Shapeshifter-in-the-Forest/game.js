// Main game file for Shapeshifter in the Forest

window.onload = function() {
  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');

  // Placeholder: draw background
  ctx.fillStyle = '#3e5d3a';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Placeholder: draw player
  ctx.fillStyle = '#fff';
  ctx.beginPath();
  ctx.arc(100, 500, 30, 0, Math.PI * 2);
  ctx.fill();

  // Placeholder: draw NPC
  ctx.fillStyle = '#f4a261';
  ctx.fillRect(300, 500, 40, 40);
};
