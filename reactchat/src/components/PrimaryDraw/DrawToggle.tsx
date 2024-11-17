import { Box, IconButton } from "@mui/material";
import ChevronLeft from "@mui/icons-material/ChevronLeft";

const DrawerToggle = () => {
    return (
        <Box
            sx={{
                height: "50px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
            }}
        >
            <IconButton>
                <ChevronLeft />
            </IconButton>
        </Box>
    );
};

export default DrawerToggle;
