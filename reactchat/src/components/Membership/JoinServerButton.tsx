import { useMembershipContext } from "../../context/MemberContext";
import { useParams } from "react-router-dom";

const JoinServerButton = () => {
    const { serverId } = useParams();
    const { joinServer, leaveServer, isLoading, error, isUserMember } = useMembershipContext();

    const handleJoinServer = async () => {
        try {
            await joinServer(Number(serverId));
            console.log("User has joined server");
        } catch (error) {
            console.log("Error joining:", error);
        }
    }
    
    const handleLeaveServer = async () => {
        try {
            await leaveServer(Number(serverId));
            console.log("User has left the server successfully!");
        } catch (error) {
            console.log("Error leaving the server:");
        }
    }

    if (isLoading) {
        return <div>Loading...</div>
    }

    // if (error) {
    //     return <div>Error: {error.message}</div>;
    // }

    return (
        <>
            ismember: {isUserMember.toString()}
            {isUserMember ? (
                <button onClick={handleLeaveServer}>Leave Server</button>
            ) : (
                <button onClick={handleJoinServer}>Join Server</button>
            )}
        </>
    );
};

export default JoinServerButton;
