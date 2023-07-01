
const quotes = [
    "The human body is a shell. It's what's inside that counts.",
    "Man is an individual only because of his intangible memory. But memory cannot be defined, yet it defines mankind.",
    "If a technological feat is possible, man will do it. Almost as if it's wired into the core of our being.",
    "What if a cyber brain could possibly generate its own ghost, create a soul all by itself?",
    "Looks without substance will leave you empty.",
    "We cling to memories as if they define us. But what we do defines us.",
    "The line between man and machine is so very blurred.",
    "The future belongs to those who believe in the beauty of their dreams.",
    "The only thing that's real is your own consciousness.",
    "My mind is human. My body is manufactured. I'm the first of my kind, but... I won't be the last.",
    "The only thing that's truly real about us is our consciousness.",
    "The real question is, what is a soul?",
    "The difference between humans and machines is that humans can choose their own destiny.",
    "The more technology we develop, the more human we become.",
    "We are all ghosts trapped in a machine.",
    "The future is not something we enter. We create it.",
    "The past is a burden we carry with us. But if we can change the present, then we can change the future.",
    "The only way to find out who you are is to lose everything.",
    "The only thing that's constant is change.",
    "The world is not what it seems.",
  ];
  
function quote() {
  randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
  document.getElementById("quote").innerHTML = randomQuote;    
}

quote()