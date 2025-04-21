export default function GibseyVault({ entries = [], onNavigate, themeColor = "#33FF33" }) {
  return (
    <aside
      className="relative w-full max-w-sm h-[884px] shadow-[0px_5px_4px_1px_#535D53] bg-black p-4"
      style={{ border: `3px solid ${themeColor}` }}
    >
      {/* Vault Grid Lines */}
      {[132, 257, 382, 507, 632, 757].map((top, i) => (
        <div
          key={i}
          className="absolute left-[3px] w-[295px] h-px border-t"
          style={{ top: `${top}px`, borderColor: "#466F46" }}
        />
      ))}

      {/* Vault Entries */}
      <div className="absolute top-10 right-4">
        {entries.length === 0 ? (
          <div
            className="text-right text-lg font-Courier Prime tracking-wide"
            style={{ color: themeColor }}
          >
            No pages saved.
          </div>
        ) : (
          entries.map((entry) => (
            <div
              key={entry.id}
              onClick={() => onNavigate?.(entry.id)}
              className="text-right text-lg font-Courier Prime tracking-wide cursor-pointer hover:underline"
              style={{ color: themeColor }}
            >
              {entry.label}
            </div>
          ))
        )}
      </div>
    </aside>
  );
}
