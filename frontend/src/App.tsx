import React, { useState, useEffect } from 'react';
import { Play, Info, Search, Bell, User } from 'lucide-react';
import axios from 'axios';

interface Movie {
  title: string;
  year: string;
  description: string;
  poster_url: string;
  filename: string;
}

const App: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [movies, setMovies] = useState<Movie[]>([]);
  const [heroMovie, setHeroMovie] = useState<Movie | null>(null);
  const [playingMovieIndex, setPlayingMovieIndex] = useState<number | null>(null);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 0);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await axios.get('/movies');
        setMovies(response.data);
        if (response.data.length > 0) {
          setHeroMovie(response.data[0]);
        }
      } catch (error) {
        console.error('Error fetching movies:', error);
      }
    };
    fetchMovies();
  }, []);

  const handlePlay = (index: number) => {
    setPlayingMovieIndex(index);
  };

  return (
    <div className="relative min-h-screen bg-cinema-black text-white">
      {/* Video Player Modal */}
      {playingMovieIndex !== null && (
        <div className="fixed inset-0 z-[100] bg-black flex items-center justify-center">
          <button 
            onClick={() => setPlayingMovieIndex(null)}
            className="absolute top-8 right-8 text-white z-[110] bg-white bg-opacity-20 p-2 rounded-full hover:bg-opacity-40"
          >
            Close
          </button>
          <video 
            src={`/stream/${playingMovieIndex}`} 
            controls 
            autoPlay 
            className="w-full h-full max-h-screen"
          />
        </div>
      )}

      {/* Navbar */}
      <nav className={`fixed top-0 w-full z-50 flex items-center justify-between px-12 py-4 transition-colors duration-300 ${isScrolled ? 'bg-cinema-black' : 'bg-transparent'}`}>
        <div className="flex items-center gap-8">
          <h1 className="text-cinema-red text-3xl font-bold tracking-tighter">CINEMA</h1>
          <ul className="hidden md:flex gap-4 text-sm font-medium text-gray-300">
            <li className="hover:text-white cursor-pointer transition">Home</li>
            <li className="hover:text-white cursor-pointer transition">TV Shows</li>
            <li className="hover:text-white cursor-pointer transition">Movies</li>
            <li className="hover:text-white cursor-pointer transition">My List</li>
          </ul>
        </div>
        <div className="flex items-center gap-6">
          <Search className="w-5 h-5 cursor-pointer" />
          <Bell className="w-5 h-5 cursor-pointer" />
          <div className="w-8 h-8 bg-cinema-red rounded cursor-pointer flex items-center justify-center">
            <User className="w-5 h-5" />
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      {heroMovie && (
        <div className="relative h-[80vh] w-full">
          <div className="absolute inset-0 bg-gradient-to-r from-cinema-black via-transparent to-transparent z-10" />
          <div className="absolute inset-0 bg-gradient-to-t from-cinema-black via-transparent to-transparent z-10" />
          <div className="absolute bottom-32 left-12 z-20 max-w-xl space-y-4">
            <h2 className="text-6xl font-bold">{heroMovie.title}</h2>
            <p className="text-lg text-gray-200">{heroMovie.description}</p>
            <div className="flex gap-4 pt-4">
              <button 
                onClick={() => handlePlay(0)}
                className="flex items-center gap-2 px-8 py-2 bg-white text-black rounded font-bold hover:bg-opacity-80 transition"
              >
                <Play className="fill-black" /> Play
              </button>
              <button className="flex items-center gap-2 px-8 py-2 bg-gray-500 bg-opacity-50 text-white rounded font-bold hover:bg-opacity-40 transition">
                <Info /> More Info
              </button>
            </div>
          </div>
          <img 
            src={heroMovie.poster_url} 
            alt="Hero Backdrop" 
            className="absolute inset-0 w-full h-full object-cover"
            onError={(e) => {
                console.error("Poster failed to load:", heroMovie.poster_url);
                (e.target as HTMLImageElement).src = "https://via.placeholder.com/1920x1080?text=Poster+Error";
            }}
          />
        </div>
      )}

      {/* Video Rows */}
      <main className="px-12 -mt-16 relative z-20 space-y-12 pb-20">
        <VideoRow title="Library" movies={movies} onPlay={handlePlay} />
        <VideoRow title="Trending Now" movies={movies} onPlay={handlePlay} />
      </main>
    </div>
  );
}

const VideoRow: React.FC<{ title: string, movies: Movie[], onPlay: (index: number) => void }> = ({ title, movies, onPlay }) => {
  return (
    <div className="space-y-4">
      <h3 className="text-xl font-bold text-gray-200">{title}</h3>
      <div className="flex gap-2 overflow-x-auto pb-4 scrollbar-hide">
        {movies.map((movie, index) => (
          <div 
            key={index} 
            onClick={() => onPlay(index)}
            className="relative flex-none w-[250px] aspect-video bg-cinema-gray rounded overflow-hidden cursor-pointer group hover:scale-110 transition duration-300 z-0 hover:z-50"
          >
            <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition flex items-center justify-center">
                <Play className="opacity-0 group-hover:opacity-100 transition w-8 h-8 fill-white" />
            </div>
            <img 
              src={movie.poster_url} 
              alt={movie.title}
              className="w-full h-full object-cover"
              onError={(e) => {
                (e.target as HTMLImageElement).src = `https://via.placeholder.com/250x140?text=${movie.title}`;
              }}
            />
            <div className="absolute bottom-0 left-0 right-0 p-2 bg-gradient-to-t from-black to-transparent opacity-0 group-hover:opacity-100 transition">
                <p className="text-xs font-bold">{movie.title}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App;
