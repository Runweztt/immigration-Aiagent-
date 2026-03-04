import React, { useState, useRef, useEffect } from 'react';

const Dashboard = ({ userData }) => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: `Hello ${userData?.full_name || 'there'}! 👋 I'm your Immigration AI Assistant. Ask me anything about visas, permits, immigration policies, or relocation processes. How can I help you today?`,
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', text: userMessage }]);
    setLoading(true);

    try {
      const token = userData?.access_token;
      const res = await fetch('http://localhost:8000/api/v1/queries/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ text: userMessage }),
      });

      if (res.ok) {
        const data = await res.json();
        setMessages((prev) => [
          ...prev,
          { role: 'assistant', text: data.response },
        ]);
      } else {
        const err = await res.json();
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            text: `⚠️ ${err.detail || 'Something went wrong. Please try again.'}`,
          },
        ]);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: '⚠️ Could not connect to the server. Please check the backend is running.',
        },
      ]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto flex flex-col" style={{ height: 'calc(100vh - 160px)' }}>
      {/* Header */}
      <div className="glass rounded-t-3xl p-5 border-b border-white/5">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold">Immigration Assistant</h2>
            <p className="text-white/40 text-xs mt-0.5">
              AI-powered guidance • {userData?.country || 'Global'}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-xs text-white/50">Online</span>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto glass border-x border-white/5 p-5 space-y-4 scrollbar-thin">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-premium-gold text-premium-dark font-medium rounded-br-md'
                  : 'bg-white/5 text-white/90 border border-white/5 rounded-bl-md'
              }`}
            >
              {msg.role === 'assistant' && (
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-5 h-5 bg-premium-gold/20 rounded-md flex items-center justify-center">
                    <span className="text-premium-gold text-[10px] font-bold">IA</span>
                  </div>
                  <span className="text-[10px] text-white/30 uppercase tracking-widest font-semibold">
                    AI Assistant
                  </span>
                </div>
              )}
              <p className="whitespace-pre-wrap">{msg.text}</p>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-white/5 border border-white/5 rounded-2xl rounded-bl-md px-4 py-3">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-5 h-5 bg-premium-gold/20 rounded-md flex items-center justify-center">
                  <span className="text-premium-gold text-[10px] font-bold">IA</span>
                </div>
                <span className="text-[10px] text-white/30 uppercase tracking-widest font-semibold">
                  AI Assistant
                </span>
              </div>
              <div className="flex gap-1.5">
                <div className="w-2 h-2 bg-white/30 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-white/30 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-white/30 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <form onSubmit={handleSend} className="glass rounded-b-3xl border-t border-white/5 p-4">
        <div className="flex gap-3">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about visas, permits, immigration policies..."
            disabled={loading}
            className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-white placeholder-white/20 focus:outline-none focus:border-premium-gold/50 transition-all disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="bg-premium-gold hover:bg-yellow-500 text-premium-dark font-bold px-6 py-3 rounded-xl transition-all shadow-lg shadow-premium-gold/20 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
        <p className="text-[10px] text-white/20 mt-2 text-center">
          Powered by LoopedAI • Responses are AI-generated and may not constitute legal advice
        </p>
      </form>
    </div>
  );
};

export default Dashboard;
