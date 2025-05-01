export default function RememberCharacterInput({ entries = [], themeColor = "#33FF33" }) {
    return (
      <div
        className="relative w-full max-w-xl h-[177px] shadow-[0px_5px_4px_1px_#535D53] bg-black p-4 font-Courier Prime text-sm tracking-wide overflow-y-scroll scrollbar-thin"
        style={{ border: `2.5px solid ${themeColor}`, color: themeColor, scrollbarColor: `${themeColor} #1A401A` }}
      >
        <ul className="space-y-2">
          {entries.length === 0 ? (
            <li className="italic">No queries submitted to this character yet.</li>
          ) : (
            entries.map((entry, index) => (
              <li
                key={index}
                className="border-b border-[#1A401A] pb-1"
                style={{ color: themeColor }}
              >
                {entry}
              </li>
            ))
          )}
        </ul>
      </div>
    );
  }
  