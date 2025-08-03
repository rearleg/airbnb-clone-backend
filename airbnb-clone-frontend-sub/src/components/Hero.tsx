import { Box, Heading, HStack, Image, Text, VStack } from "@chakra-ui/react";
import { Link } from "react-router-dom";

interface IComicProp {
  characterId: number;
  key: number;
  name: string;
  description: string;
  tumbnail: string;
  extension: string;
}

export default function Hero({
  characterId,
  name,
  tumbnail,
  extension,
  description,
}: IComicProp) {
  const image =
    `${tumbnail}.${extension}` ===
    "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available.jpg"
      ? "https://cdn.marvel.com/u/prod/marvel/i/mg/4/30/687684046af5e/portrait_uncanny.jpg"
      : `${tumbnail}.${extension}`;
  //src="http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available.jpg"
  return (
    <Link to={`/characters/${characterId}`}>
      <Box>
        <VStack>
          <Box
            position={"relative"}
            overflow={"hidden"}
            mb={4}
            rounded={"2xl"}
            w={"300px"}
            h={"400px"}
          >
            <Image
              objectFit="cover"
              w={"100%"}
              h={"100%"}
              minH={"280"}
              src={image}
            />
          </Box>
          <Box>
            <Heading fontSize={"xl"}>{name}</Heading>
          </Box>
        </VStack>
      </Box>
    </Link>
  );
}
