export default function ReadPage({ themeColor = "#33FF33", symbol = "" }) {
  return (
    <div
      className="relative w-full h-60 p-4 flex flex-col justify-between shadow-[2px_2px_0px] overflow-y-scroll scrollbar-thin font-mono text-sm tracking-wide"
      style={{ border: `2px solid ${themeColor}`, boxShadow: `2px 2px 0px ${themeColor}`, color: themeColor, scrollbarColor: `${themeColor} #1A401A` }}
    >
      {/* Symbol Tag in Corner */}
      {symbol && (
        <div
          className="absolute top-2 left-2 w-6 h-6 rounded-full"
          style={{ backgroundImage: `url(/symbols/${symbol}.svg)`, backgroundSize: "cover" }}
          title={symbol}
        ></div>
      )}

      {/* Navigation Arrows */}
      <div className="absolute bottom-2 left-0 w-full flex justify-between items-center px-4">
        <span
          className="text-2xl"
          style={{ color: themeColor, textShadow: `2px 2px 0px ${themeColor}` }}
        >
          ←
        </span>
        <span
          className="text-2xl"
          style={{ color: themeColor, textShadow: `2px 2px 0px ${themeColor}` }}
        >
          →
        </span>

        {/* Vault Save Icon */}
        <div
          className="text-xl"
          style={{ color: themeColor, textShadow: `2px 2px 0px ${themeColor}` }}
        >
          ⎘
        </div>
      </div>
    </div>
  );
}
