export default function optionTitleFiler(str: string): string {
  return str.replace(/[A-Z]/g, (v) => {
    return " " + v;
  });
}
