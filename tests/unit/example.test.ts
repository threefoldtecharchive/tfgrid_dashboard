function starter(): number {
  return window.config.network;
}

test("Check the selected network", () => {
  expect(starter()).toBe("dev");
});
