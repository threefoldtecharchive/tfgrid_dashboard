export default function toTeraOrGiga(value?: string) {
  if (!value) return "0";

  const val = +value;
  if (val === 0 || isNaN(val)) return "0";

  if (val < 1e9) return val.toString();

  let gb = Math.round(val / 1e7) / 1e2;

  if (gb < 1000) return `${gb} GB`;

  gb /= 10;
  gb = Math.round(gb) / 1e2;

  if (gb < 1000) return `${gb} TB`;

  gb /= 10;
  gb = Math.round(gb) / 1e2;
  return `${gb} PB`;
}
