export default function GibseyVaultHeader({ themeColor = "#33FF33" }) {
  return (
    <header
      className="w-full max-w-sm h-28 shadow-[0px_5px_4px_1px_#535D53] bg-black flex items-center justify-center px-4"
      style={{ border: `3px solid ${themeColor}` }}
    >
      <h2
        className="text-lg md:text-xl font-Courier Prime tracking-widest text-center"
        style={{ color: themeColor }}
      >
        The Gibsey Vault
      </h2>
    </header>
  );
}
