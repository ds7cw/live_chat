import {
    List,
    ListItem,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Box,
    Typography,
} from "@mui/material";
import useCrud from "../../hooks/useCrud";
import React, { useEffect } from "react";
import { ListItemAvatar } from "@mui/material";
import { MEDIA_URL } from "../../config";
import { Link } from "react-router-dom";

interface Server {
    id: number;
    name: string;
    category: string;
    icon: string;
}

type Props = {
    open: boolean;
};

const PopularChannels: React.FC<Props> = ({ open }) => {
    const { dataCRUD, error, isLoading, fetchData } = useCrud<Server>(
        [], 
        "/server/select/",
    );

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <>
            <Box
                sx={{
                    height: 50,
                    p: 2,
                    display: "flex",
                    alignItems: "center",
                    flex: "1 1 100%",
                }}
            >
                <Typography 
                    sx={{
                        display: open ? "block" : "none"
                    }}>
                    Popular
                </Typography>
            </Box>
            <List>
                {dataCRUD.map((item) => (
                    <ListItem key={item.id} disablePadding
                        sx={{display: "block"}}
                        dense={true}
                    >
                        <Link to={`/server/${item.id}`}
                            style={{ textDecoration: "none", color: "inherit" }}
                        >
                            {item.name}
                        </Link>
                    </ListItem>
                ))}
            </List>
        </>
    );
};
export default PopularChannels;