// Smoke test for the csharp-skills dotnet gate.
// Proves the toolchain works; per-rule snippets opt in via <!-- compile -->.
using var cts = new CancellationTokenSource();
cts.Cancel();
Console.WriteLine("csharp-skills gate ok");
