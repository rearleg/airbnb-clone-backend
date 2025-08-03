import { createBrowserRouter } from "react-router-dom";
import Root from "./components/Root";
import Home from "./routes/Home";
import NotFound from "./routes/NotFound";
import Characters from "./routes/Characters";
import ComicDetail from "./routes/ComicDetail";
import ComicDetailCharacter from "./routes/ComicDetailCharacter";
import CharacterDetail from "./routes/CharacterDetail";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <NotFound />,
    children: [
      {
        path: "",
        element: <Home />,
      },
      {
        path: "comics/:comicId",
        element: <ComicDetail />,
      },
      {
        path: "comics/:comicId/characters",
        element: <ComicDetailCharacter />,
      },
      {
        path: "characters",
        element: <Characters />,
      },
      {
        path: "characters/:characterId",
        element: <CharacterDetail />,
      },
    ],
  },
]);

export default router;
