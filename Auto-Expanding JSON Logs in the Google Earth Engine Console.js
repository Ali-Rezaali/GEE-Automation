// Finds and Clicks Every Leaf Element In The GEE Console Containing Exact Text 'JSON'

const jsonButtons = Array.from(document.querySelectorAll('*')).filter(
  el => el.children.length === 0 && el.textContent.trim() === 'JSON'
);

console.log(`Found ${jsonButtons.length} JSON buttons. Clicking...`);

jsonButtons.forEach((btn, index) => {
  setTimeout(() => {
    btn.click();
  }, index * 30); // 30ms Stagger Prevents UI Freeze
});
