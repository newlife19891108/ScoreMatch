# ScoreMatch
An implementation for finding the best matching audio for a given score.It provides metadata matching and audio matching seperately.Full-metadata matching is implemented based on [extractArtist](http://developer.echonest.com/docs/v4/artist.html#extract-beta) method of the Echonest api.Audio matching is done based on dynamic time warping with chroma feature sequences.MuseScore API is used for the scores. Echonest and Spotify APIs are used for extracting and examining audio sources
#Usage
First create score based on a MuseScore score id
```python
score = create_score(score_id) 
```
For full-metadata matching on score
```python
score.metadata_match()
```
This will return a single result as [EchonestSong](https://github.com/woryzower/ScoreMatch/blob/master/ScoreMatch/apiwrappers/echonestsong.py) or [SpotifyTrack](https://github.com/woryzower/ScoreMatch/blob/master/ScoreMatch/apiwrappers/spotifytrack.py) and None if no song is matched.

  For audio matching first generate possible candidate queries.Then, get tracks for list of tracks for any candidate query.Then, rank tracks with respect to similarity to the score.
```python
queries = score.get_queries()
tracks = query_spotify(query[0])
ranking = rank_analyzables(score, tracks, 'full')
```
ranking is list of 2-tuples (matched_track,matching_score)
```python
best_track = ranking[0][0]
best_score = ranking[0][1]
```

The algorithm has two modes as full and partial.In full mode, chroma sequence of full candidate audio is used for the matching.In partial mode chroma sequence is extracted from 30 seconds spotify preview audio

```python
ranking = rank_analyzables(score, tracks, 'partial')
ranking = rank_analyzables(score, tracks, 'full')
```
#Dependencies
[rpy](http://rpy.sourceforge.net/) and [rdtw](http://dtw.r-forge.r-project.org/)
[sonic-annotator](http://www.vamp-plugins.org/sonic-annotator/) for partial mode 
[mido](https://pypi.python.org/pypi/mido/1.1.3)
[pyechonest](https://github.com/echonest/pyechonest)
