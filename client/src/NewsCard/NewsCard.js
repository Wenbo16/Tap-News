import './NewsCard.css';

import React from 'react';
import Auth from '../Auth/Auth';

class NewsCard extends React.Component {
    constructor() {
        super();
        this.state = {likes:false};
        this.redirectToUrl = this.redirectToUrl.bind(this);
        this.sendUserLikes = this.sendUserLikes.bind(this);
    }


    redirectToUrl(event) {
        event.preventDefault();
        this.sendClickLog();
        window.open(this.props.news.url, '_blank');
    }


    sendClickLog() {
        let url = 'http://localhost:3000/news/userId/' + encodeURIComponent(Auth.getEmail())
                  + '/newsId/' + encodeURIComponent(this.props.news.digest);
        console.log(url);
        let request = new Request(url, {
            method: 'GET',
            headers: {
                'Authorization': 'bearer ' + Auth.getToken(),
            },
            cache: false
        });

        fetch(request)
            .then((res) => {
                console.log(res);
                return res.json();
            }).then((similarNews) => {
                if(!similarNews.length !== 0){
                    this.props.getSimilarNews(similarNews);
                }
            });
    }

    sendUserLikes() {
        this.setState({likes:!this.state.likes});
        let url = 'http://localhost:3000/news/userLikes/userId/' + Auth.getEmail() + '/newsId/' + this.props.news.digest;
        let request = new Request(encodeURI(url), {
            method: 'POST',
            headers: {
                'Authorization': 'bearer ' + Auth.getToken(),
            },
            cache: false
        });
        fetch(request);
    }



    render() {
        const isFavorite = this.state.likes;

        return (
            <div className="news-container">
                <div className='row'>
                    <div className='col s4 fill'>
                        <img src={this.props.news.urlToImage} alt='news' />
                    </div>
                    <div className="col s8">
                        <div className="news-intro-col">
                            <div className="news-intro-panel">
                                <h4>{this.props.news.title}</h4>
                                <div className="news-description">
                                    <p>{this.props.news.description}</p>
                                    <div>
                                        {this.props.news.source != null &&
                                        <div className='chip light-blue news-chip'>{this.props.news.source}</div>} {this.props.news.reason != null &&
                                        <div className='chip light-green news-chip'>{this.props.news.reason}</div>} {this.props.news.time != null &&
                                        <div className='chip amber news-chip'>{this.props.news.time}</div>}

                                        <button className="btn waves-effect waves-light pull right" onClick={this.redirectToUrl}>Detail
                                        </button>
                                        {isFavorite ? 
                                            (<button className="btn waves-effect light-green pull right" onClick={()=> this.sendUserLikes()}> Favorite
                                             </button>) 
                                            :
                                            (<button className="btn waves-effect waves-light pull right" onClick={()=> this.sendUserLikes()}> Like
                                             </button>)}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default NewsCard;
