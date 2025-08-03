import { useQuery } from "@tanstack/react-query"
import { listComicCharacters } from "../api";
import { useParams } from "react-router-dom";
import { Box, Grid, Heading, Image, VStack } from "@chakra-ui/react";
import Hero from "../components/Hero";
import { CharactersResponse } from "../types";



export default function ComicDetailCharacter() {
  const { comicId } = useParams()
  const { isLoading, data} = useQuery<CharactersResponse>({
    queryKey:["comics", comicId, "characters" ] ,
    queryFn: listComicCharacters
  })
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
      {results?.map((character) => (
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