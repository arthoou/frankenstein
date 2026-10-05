s = IO.read(:stdio, :eof) |> String.trim()
IO.write(s <> " -> Elixir")
