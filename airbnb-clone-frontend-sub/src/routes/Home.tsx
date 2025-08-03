import { Grid } from "@chakra-ui/react";
import Comic from "../components/Comic";
import { listComics } from "../api";
import { ComicsResponse, ComicsResult } from "../types";
import { useQuery } from "@tanstack/react-query";

export default function Home() {
  const { isLoading, data } = useQuery<ComicsResponse>({
    queryKey: ["comics"],
    queryFn: listComics,
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
      {results?.slice(2).map((comic) => (
        <Comic
          key={comic.id}
          comicId={comic.id}
          title={comic.title}
          tumbnail={comic.thumbnail.path}
          extension={comic.thumbnail.extension}
        />
      ))}
    </Grid>
  );
}

// id, title, series, thumbnail(path, extension),
