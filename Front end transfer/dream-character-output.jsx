import { useEffect, useRef, useState } from "react";

export default function DreamCharacterOutput({ responseText = "", themeColor = "#33FF33" }) {
  const [displayedText, setDisplayedText] = useState("");
  const caretRef = useRef(null);

  useEffect(() => {
    setDisplayedText("");
    let i = 0;
    const interval = setInterval(() => {
      if (i < responseText.length) {
        setDisplayedText((prev) => prev + responseText[i]);
        i++;
      } else {
        clearInterval(interval);
      }
    }, 30);

    return () => clearInterval(interval);
  }, [responseText]);

  useEffect(() => {
    const caret = caretRef.current;
    if (caret) {
      const span = document.createElement("span");
      span.style.visibility = "hidden";
      span.style.position = "absolute";
      span.style.whiteSpace = "pre";
      span.style.font = window.getComputedStyle(caret).font;
      span.textContent = displayedText;
      document.body.appendChild(span);
      const width = span.getBoundingClientRect().width;
      caret.style.left = `${width}px`;
      document.body.removeChild(span);
    }
  }, [displayedText]);

  return (
    <div
      className="relative w-full max-w-xl h-[229px] overflow-y-scroll shadow-[0px_5px_4px_1px_#535D53] bg-black p-4 font-Courier Prime text-sm tracking-wide scrollbar-thin"
      style={{ border: `2.5px solid ${themeColor}`, color: themeColor, scrollbarColor: `${themeColor} #1A401A` }}
    >
      {/* Typing Response */}
      <div className="relative">
        {displayedText}
        <span
          ref={caretRef}
          className="absolute top-0 animate-pulse"
          style={{ color: themeColor }}
        >
          |
        </span>
      </div>
    </div>
  );
}
