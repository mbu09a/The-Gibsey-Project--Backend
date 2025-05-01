import { useEffect, useRef } from "react";

const chapters = [
  { id: 0, title: "an author's preface", color: "#33FF33", symbol: "symbol-author" },
  { id: 1, title: "London Fox Who Vertically Disintegrates", color: "#FF3333", symbol: "symbol-london" },
  { id: 2, title: "An Unexpected Disappearance Ch. 1-6", color: "#00A2FF", symbol: "symbol-glyph" },
  { id: 3, title: "An Expected Appearance Ch. 1-3", color: "#FFFF33", symbol: "symbol-bafflemint" },
  { id: 4, title: "Jacklyn Variance, The Watcher, Is Watched", color: "#FF00FF", symbol: "symbol-jacklyn" },
  { id: 5, title: "the Last Auteur", color: "#00FFAA", symbol: "symbol-oren" },
  { id: 6, title: "Gibseyan Mysticism and Its Symbolism", color: "#7A3CFF", symbol: "symbol-old-natalie" },
  { id: 7, title: "Princhetta Who Thinks Herself Alive", color: "#AAAAAA", symbol: "symbol-princhetta" },
  { id: 8, title: "Petition For Bankruptcy: Chapter 11", color: "#FFFFFF", symbol: "symbol-copyright" },
  { id: 9, title: "The Tempestuous Storm", color: "#CC66FF", symbol: "symbol-new-natalie" },
  { id: 10, title: "Arieol Owlist Who Wants to Achieve Agency", color: "#99CCFF", symbol: "symbol-arieol" },
  { id: 11, title: "The Biggest Shit of All Time", color: "#FF3385", symbol: "symbol-parlance" },
  { id: 12, title: "An Expected Appearance Chap. 4-6", color: "#FFB000", symbol: "symbol-manny" },
  { id: 13, title: "An Unexpected Disappearance Chap. 7-11", color: "#00FFFF", symbol: "symbol-shamrock" },
  { id: 14, title: "Todd Fishbone Who Dreams of Synchronistic Extraction", color: "#FF7744", symbol: "symbol-todd" },
  { id: 15, title: "The Author's Preface", color: "#BFFF00", symbol: "symbol-the-author" },
];

export default function ChapterNavigation({ onSelectChapter }) {
  const navRef = useRef(null);

  useEffect(() => {
    const nav = navRef.current;
    if (!nav) return;

    const handleKeyDown = (e) => {
      if (document.activeElement === document.body) {
        if (e.key === "ArrowDown") nav.scrollBy({ top: 40, behavior: "smooth" });
        if (e.key === "ArrowUp") nav.scrollBy({ top: -40, behavior: "smooth" });
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  return (
    <aside
      ref={navRef}
      className="w-48 h-full overflow-y-scroll border-r-2 border-green-500 p-2 space-y-4 bg-black scrollbar-thin scrollbar-thumb-green-500 hover:overflow-y-auto"
    >
      {chapters.map((chapter) => (
        <div
          key={chapter.id}
          className="text-center text-sm font-mono leading-tight tracking-wide cursor-pointer hover:underline"
          style={{ color: chapter.color }}
          onClick={() =>
            onSelectChapter({
              id: chapter.id,
              title: chapter.title,
              color: chapter.color,
              symbol: chapter.symbol,
            })
          }
        >
          {chapter.title}
        </div>
      ))}
    </aside>
  );
}
