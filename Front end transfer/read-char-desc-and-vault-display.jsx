const characterDescriptions = {
    0: "An Author is the fractured voice that echoes across all others.",
    1: "London Fox is a trickster of vertical disintegration, unraveling media itself.",
    2: "Glyph Marrow investigates disappearances and semantic decay.",
    3: "Phillip Bafflemint builds order from narrative chaos.",
    4: "Jackyln Variance watches the watchers.",
    5: "Oren Progresso is the final auteur.",
    6: "Old Natalie Weissman is a mystic scholar of Gibsey’s forgotten patterns.",
    7: "Princhetta believes she’s alive—and maybe she is.",
    8: "Cop-E-Right protects, archives, and obstructs.",
    9: "New Natalie Weissman seeks vengeance in recursive storms.",
    10: "Arieol Owlist longs for real agency in a synthetic world.",
    11: "Jack Parlance is a producer of unbearable legends.",
    12: "Manny Valentinas organizes expectation.",
    13: "Shamrock Stillman plays with disappearance and fame.",
    14: "Todd Fishbone dreams of synchronistic extraction.",
    15: "The Author is the echo at the end of time."
  };
  
  export default function ReadCharDescVaultDisplay({ character }) {
    const themeColor = character?.color || "#33FF33";
    const description = character ? characterDescriptions[character.id] : "Select a character to see their description.";
    const symbol = character?.symbol;
  
    return (
      <div
        className="relative w-full max-w-xl h-[413px] shadow-[0px_5px_4px_1px_#535D53] bg-black p-6 font-Courier Prime text-sm tracking-wide overflow-y-scroll scrollbar-thin"
        style={{ border: `2.5px solid ${themeColor}`, color: themeColor, scrollbarColor: `${themeColor} #1A401A` }}
      >
        {/* Symbol Tag in Bottom-Right Corner */}
        {symbol && (
          <div
            className="absolute bottom-2 right-2 w-6 h-6 rounded-full"
            style={{ backgroundImage: `url(/symbols/${symbol}.svg)`, backgroundSize: "cover" }}
            title={symbol}
          ></div>
        )}
  
        {description}
      </div>
    );
  }
  