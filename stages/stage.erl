main(_Args) ->
    Data = read_all(<<>>),
    S = string:trim(Data),
    io:format("~s -> Erlang", [S]).

read_all(Acc) ->
    case io:get_line(standard_io, "") of
        eof -> Acc;
        {error, _} -> Acc;
        Line -> read_all(<<Acc/binary, (unicode:characters_to_binary(Line))/binary>>)
    end.
