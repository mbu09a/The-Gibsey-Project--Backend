import { useState, useRef, useEffect } from "react";

export default function WriteCharacterUserInput({ onSubmitQuery, themeColor = "#33FF33" }) {
  const [text, setText] = useState("");
  const inputRef = useRef(null);
  const caretRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    const query = text.trim();
    if (!query) return;
    onSubmitQuery?.(query);
    setText("");
  };

  useEffect(() => {
    const input = inputRef.current;
    const caret = caretRef.current;
    if (input && caret) {
      const span = document.createElement("span");
      span.style.visibility = "hidden";
      span.style.position = "absolute";
      span.style.whiteSpace = "pre";
      span.style.font = window.getComputedStyle(input).font;
      span.textContent = text;
      document.body.appendChild(span);
      const width = span.getBoundingClientRect().width;
      caret.style.left = `${width}px`;
      document.body.removeChild(span);
    }
  }, [text]);

  return (
    <form
      onSubmit={handleSubmit}
      className="relative w-full max-w-xl h-[138px] shadow-[0px_5px_4px_1px_#535D53] bg-black flex items-center px-6"
      style={{ border: `3px solid ${themeColor}` }}
    >
      {/* Input Field */}
      <div className="relative flex-grow font-Courier Prime text-lg tracking-wide" style={{ color: themeColor }}>
        <input
          type="text"
          ref={inputRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="w-full bg-transparent border-none outline-none caret-transparent pr-8"
          placeholder="Ask a question to this character..."
        />
        <span
          ref={caretRef}
          className="absolute top-0 animate-pulse"
          style={{ color: themeColor }}
        >
          |
        </span>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        className="absolute bottom-6 right-6 w-[65.29px] h-[27.42px] font-Courier Prime text-sm hover:bg-[#1f4f1f]"
        style={{ backgroundColor: "#164016", border: `1px solid ${themeColor}`, color: themeColor, boxShadow: "0px 5px 4px rgba(93,104,93,0.70)" }}
      >
        Ask
      </button>
    </form>
  );
}
