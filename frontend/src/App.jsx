import "./index.css";
import ChatWidget from "./ChatWidget";

function App() {
  return (
    <div className="app">

      <section className="hero">

        <h1>E2M Solutions</h1>

        <h2>AI-Powered Digital Solutions</h2>

        <p>
          Helping agencies grow with AI, automation,
          web development and digital marketing.
        </p>

        <button className="hero-btn">
          Ask Our AI
        </button>

      </section>

      <section className="services">

        <div className="card">
          🤖
          <h3>AI Development</h3>
          <p>Custom AI applications and intelligent automation.</p>
        </div>

        <div className="card">
          💻
          <h3>Web Development</h3>
          <p>Scalable websites and modern web applications.</p>
        </div>

        <div className="card">
          📈
          <h3>Digital Marketing</h3>
          <p>SEO, PPC and growth strategies for agencies.</p>
        </div>

      </section>
      <ChatWidget />

    </div>
  );
}

export default App;