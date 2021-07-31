import React,{ Component } from 'react';

export default class Room extends Component {
    constructor(props){
        super(props);
        this.state = {
            votesToSkip: 2,
            guestCanPause: false,
            isHost: false,
            };
            this.roomCode = this.props.match.params.roomCode;
            this.getRoomDetails ();
        }
    getRoomDetails() {
        fetch('/api/get-room'+'?code=' + this.roomCode).then((response)=> response.json()).then((data)=>{
            this.setState({
                votesToSkip: data.votes_to_skip,
                guestCanPause: data.guestCanPause,
                isHost: data.is_host,
            });
        });
    }

    render() {
        return <div>
            <h3>{this.roomCode}</h3>
            <p>Votes :{this.state.votesToSkip}</p>
            <p>Guest can pause :{this.state.guestCanPause}</p>
            <p>Host :{this.state.host}</p>
        </div>
    }
}