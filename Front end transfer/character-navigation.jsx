import { useEffect, useRef } from "react";

const characters = [
  { id: 0, name: "an author", color: "#33FF33", symbol: "symbol-author" },
  { id: 1, name: "London Fox", color: "#FF3333", symbol: "symbol-london" },
  { id: 2, name: "Glyph Marrow", color: "#00A2FF", symbol: "symbol-glyph" },
  { id: 3, name: "Phillip Bafflemint", color: "#FFFF33", symbol: "symbol-bafflemint" },
  { id: 4, name: "Jackyln Variance", color: "#FF00FF", symbol: "symbol-jacklyn" },
  { id: 5, name: "Oren Progresso", color: "#00FFAA", symbol: "symbol-oren" },
  { id: 6, name: "Old Natalie Weissman", color: "#7A3CFF", symbol: "symbol-old-natalie" },
  { id: 7, name: "Princhetta", color: "#AAAAAA", symbol: "symbol-princhetta" },
  { id: 8, name: "Cop-E-Right", color: "#FFFFFF", symbol: "symbol-copyright" },
  { id: 9, name: "New Natalie Weissman", color: "#CC66FF", symbol: "symbol-new-natalie" },
  { id: 10, name: "Arieol Owlist", color: "#99CCFF", symbol: "symbol-arieol" },
  { id: 11, name: "Jack Parlance", color: "#FF3385", symbol: "symbol-parlance" },
  { id: 12, name: "Manny Valentinas", color: "#FFB000", symbol: "symbol-manny" },
  { id: 13, name: "Shamrock Stillman", color: "#00FFFF", symbol: "symbol-shamrock" },
  { id: 14, name: "Todd Fishbone", color: "#FF7744", symbol: "symbol-todd" },
  { id: 15, name: "The Author", color: "#BFFF00", symbol: "symbol-the-author" },
];

export default function CharacterNavigation({ onSelectCharacter }) {
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
      className="w-48 h-full overflow-y-scroll border-l-2 border-green-500 p-2 space-y-4 bg-black scrollbar-thin scrollbar-thumb-green-500 hover:overflow-y-auto"
    >
      {characters.map((character) => (
        <div
          key={character.id}
          onClick={() =>
            onSelectCharacter({
              id: character.id,
              name: character.name,
              color: character.color,
              symbol: character.symbol,
            })
          }
          className="text-center text-sm font-mono leading-tight tracking-wide cursor-pointer hover:underline"
          style={{ color: character.color }}
        >
          {character.name}
        </div>
      ))}
    </aside>
  );
}
