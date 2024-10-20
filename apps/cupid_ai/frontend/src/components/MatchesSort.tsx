import * as React from "react";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";

export default function MatchesSort() {
  const [sort, setSort] = React.useState<string>("urgency");

  const handleChange = (event: SelectChangeEvent) => {
    setSort(event.target.value);
  };

  return (
    <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
      <InputLabel id="sort-label">Sort</InputLabel>
      <Select
        labelId="sort-label"
        id="sort"
        value={sort}
        label="Sort"
        onChange={handleChange}
      >
        <MenuItem value="urgency">Urgency</MenuItem>
        <MenuItem value="distance">Distance</MenuItem>
        <MenuItem value="attractiveness">Attractiveness</MenuItem>
      </Select>
    </FormControl>
  );
}
