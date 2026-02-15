import React, { useState, useEffect, useRef } from 'react';
import { Play, Info, Search, Bell, User } from 'lucide-react';
import axios from 'axios';

interface Movie {
  id: number;
  title: string;
  year: string;
  description: string;
  poster_url: string;
  backdrop_url: string;
  filename: string;
  genre: string;
  progress: number;
  duration: number;
}

const App: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [movies, setMovies] = useState<Movie[]>([]);
  const [activeCategory, setActiveCategory] = useState('Home');
  const [heroMovie, setHeroMovie] = useState<Movie | null>(null);
  const [playingMovieIndex, setPlayingMovieIndex] = useState<number | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 0);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const fetchMovies = async () => {
    try {
      const response = await axios.get('/movies');
      setMovies(response.data);
      if (response.data.length > 0 && !heroMovie) {
        setHeroMovie(response.data[0]);
      }
    } catch (error) {
      console.error('Error fetching movies:', error);
    }
  };

  useEffect(() => {
    fetchMovies();
  }, []);

  const handlePlay = (index: number) => {
    setPlayingMovieIndex(index);
  };

  // Resume logic
  useEffect(() => {
    if (playingMovieIndex !== null && videoRef.current) {
      const movie = movies[playingMovieIndex];
      if (movie && movie.progress > 0) {
        videoRef.current.currentTime = movie.progress;
      }
    }
  }, [playingMovieIndex]);

  // Progress tracking logic
  useEffect(() => {
    let interval: any;
    if (playingMovieIndex !== null && videoRef.current) {
      interval = setInterval(() => {
        if (videoRef.current && playingMovieIndex !== null) {
          const currentTime = Math.floor(videoRef.current.currentTime);
          const duration = Math.floor(videoRef.current.duration);
          const movieId = movies[playingMovieIndex].id;
          axios.post(`/progress/${movieId}?seconds=${currentTime}&duration=${duration}`).catch(err => console.error("Failed to save progress", err));
        }
      }, 5000); // Save every 5 seconds
    }
    return () => clearInterval(interval);
  }, [playingMovieIndex]);

  const handleVideoEnded = () => {
    if (playingMovieIndex !== null && playingMovieIndex < movies.length - 1) {
      // Autoplay next episode/movie
      setPlayingMovieIndex(playingMovieIndex + 1);
    } else {
      setPlayingMovieIndex(null);
    }
  };

  const filteredMovies = movies.filter(m => {
    if (activeCategory === 'Home') return true;
    if (activeCategory === 'Movies') return !m.filename.toLowerCase().includes('s0') && !m.filename.toLowerCase().includes('e0');
    if (activeCategory === 'TV Shows') return m.filename.toLowerCase().includes('s0') || m.filename.toLowerCase().includes('e0');
    return true;
  });

  const genres = Array.from(new Set(movies.map(m => m.genre || "Uncategorized")));

  return (
    <div className="relative min-h-screen bg-cinema-black text-white">
      {/* Video Player Modal */}
      {playingMovieIndex !== null && (
        <div className="fixed inset-0 z-[100] bg-black flex items-center justify-center">
          <button 
            onClick={() => {
                setPlayingMovieIndex(null);
                fetchMovies(); // Refresh list to update progress bars/state
            }}
            className="absolute top-8 right-8 text-white z-[110] bg-white bg-opacity-20 p-2 rounded-full hover:bg-opacity-40"
          >
            Close
          </button>
          <video 
            ref={videoRef}
            src={`/stream/${movies[playingMovieIndex].id}`} 
            controls 
            autoPlay 
            onEnded={handleVideoEnded}
            className="w-full h-full max-h-screen"
          />
        </div>
      )}

      {/* Navbar */}
      <nav className={`fixed top-0 w-full z-50 flex items-center justify-between px-12 py-4 transition-colors duration-300 ${isScrolled ? 'bg-cinema-black' : 'bg-transparent'}`}>
        <div className="flex items-center gap-8">
          <h1 className="text-cinema-red text-3xl font-bold tracking-tighter cursor-pointer" onClick={() => setActiveCategory('Home')}>CINEMA</h1>
          <ul className="hidden md:flex gap-4 text-sm font-medium text-gray-300">
            {['Home', 'TV Shows', 'Movies', ...genres].map(cat => (
                <li 
                    key={cat}
                    onClick={() => setActiveCategory(cat)}
                    className={`${activeCategory === cat ? 'text-white font-bold' : ''} hover:text-white cursor-pointer transition`}
                >
                    {cat}
                </li>
            ))}
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
      {heroMovie && activeCategory === 'Home' && (
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
                (e.target as HTMLImageElement).src = "https://via.placeholder.com/1920x1080?text=Poster+Error";
            }}
          />
        </div>
      )}

      {/* Video Rows */}
      <main className={`px-12 ${activeCategory === 'Home' ? '-mt-16' : 'pt-24'} relative z-20 space-y-12 pb-20`}>
        {activeCategory === 'Home' ? (
            genres.map(genre => (
                <VideoRow 
                    key={genre}
                    title={genre} 
                    movies={movies.filter(m => m.genre === genre)} 
                    onPlay={(index) => {
                        const genreMovies = movies.filter(m => m.genre === genre);
                        const actualIndex = movies.findIndex(m => m.id === genreMovies[index].id);
                        handlePlay(actualIndex);
                    }} 
                />
            ))
        ) : (
            <VideoRow title={activeCategory} movies={filteredMovies} onPlay={(index) => {
                const actualIndex = movies.findIndex(m => m.id === filteredMovies[index].id);
                handlePlay(actualIndex);
            }} />
        )}
        
        {activeCategory === 'Home' && (
            <VideoRow title="Continue Watching" movies={movies.filter(m => m.progress > 0).sort((a,b) => b.id - a.id)} onPlay={(index) => {
                const continueMovies = movies.filter(m => m.progress > 0).sort((a,b) => b.id - a.id);
                const actualIndex = movies.findIndex(m => m.id === continueMovies[index].id);
                handlePlay(actualIndex);
            }} />
        )}
      </main>
    </div>
  );
}

const VideoRow: React.FC<{ title: string, movies: Movie[], onPlay: (index: number) => void }> = ({ title, movies, onPlay }) => {
  if (movies.length === 0) return null;
  
  return (
    <div className="space-y-4">
      <h3 className="text-xl font-bold text-gray-200">{title}</h3>
      <div className="flex gap-2 overflow-x-auto pb-4 scrollbar-hide">
        {movies.map((movie, index) => (
          <div 
            key={movie.id} 
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
                {movie.progress > 0 && movie.duration > 0 && (
                    <div className="w-full h-1 bg-gray-600 mt-1 rounded-full overflow-hidden">
                        <div 
                            className="h-full bg-cinema-red" 
                            style={{ width: `${(movie.progress / movie.duration) * 100}%` }}
                        ></div>
                    </div>
                )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App;
