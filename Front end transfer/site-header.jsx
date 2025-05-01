export default function PageHeader({ themeColor = "#33FF33" }) {
  return (
    <header
      className="w-full max-w-5xl h-20 shadow-[0px_5px_4px_1px_#535D53] bg-black flex items-center px-6"
      style={{ border: `3px solid ${themeColor}` }}
    >
      <h1
        className="text-xl md:text-2xl font-Courier Prime tracking-wide leading-tight"
        style={{ color: themeColor }}
      >
        The Entrance Way: Into the Wonderful Worlds of Gibsey
      </h1>
    </header>
  );
}