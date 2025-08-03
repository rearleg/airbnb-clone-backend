import { Grid } from "@chakra-ui/react";
import Hero from "../components/Hero";
import { listCharacters } from "../api";
import { CharactersResponse } from "../types";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";

export default function Character() {
  const { isLoading, data } = useQuery<CharactersResponse>({
    queryKey: ["characters"],
    queryFn: listCharacters,
  });
  const results = data?.data.results;
  return (
    <Grid
      mt={5}
      px={40}
      columnGap={6}
      rowGap={12}
      templateColumns={{
        sm: "1fr",
        md: "1fr 1fr",
        lg: "repeat(3, 1fr)",
        xl: "repeat(4, 1fr)",
        "2xl": "repeat(5, 1fr)",
      }}
    >
      {results?.slice(2).map((character) => (
        <Hero
          key={character.id}
          characterId={character.id}
          name={character.name}
          description={character.description}
          tumbnail={character.thumbnail.path}
          extension={character.thumbnail.extension}
        />
      ))}
    </Grid>
  );
}

// id, title, series, thumbnail(path, extension),
