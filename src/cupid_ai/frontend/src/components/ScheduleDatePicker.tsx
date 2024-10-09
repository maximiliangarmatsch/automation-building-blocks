import { useState } from "react";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { LocalizationProvider, DatePicker } from "@mui/x-date-pickers";
import Button from "@mui/material/Button";
import { format, parse } from "date-fns";

type AvailableDate = {
  date: string;
  startTime: string;
  endTime: string;
};

interface ScheduleDatePickerProps {
  availableDates: AvailableDate[];
}

const ScheduleDatePicker = (props: ScheduleDatePickerProps) => {
  const { availableDates } = props;
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [selectedTime, setSelectedTime] = useState("");

  const isDateAvailable = (date) => {
    return availableDates.some(
      (availableDate) => format(date, "yyyy-MM-dd") === availableDate.date
    );
  };

  const handleDateChange = (newDate) => {
    setSelectedDate(newDate);
    setSelectedTime("");
  };

  const getAvailableTimesForDate = (date) => {
    const selectedDateInfo = availableDates.find(
      (d) => d.date === format(date, "yyyy-MM-dd")
    );
    if (!selectedDateInfo) return [];

    const startTime = parse(selectedDateInfo.startTime, "HH:mm", new Date());
    const endTime = parse(selectedDateInfo.endTime, "HH:mm", new Date());

    const times: any[] = [];
    let currentTime = startTime;
    while (currentTime <= endTime) {
      times.push(format(currentTime, "HH:mm"));
      currentTime = new Date(currentTime.getTime() + 30 * 60000); // Add 30 minutes
    }
    return times;
  };

  const handleTimeChange = (event) => {
    setSelectedTime(event.target.value);
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <div className="flex flex-col space-y-4">
        <DatePicker
          label="Select Date"
          value={selectedDate}
          onChange={handleDateChange}
          shouldDisableDate={(date) => !isDateAvailable(date)}
          format="dd/MM/yyyy" // Display format
        />
        {selectedDate && (
          <select
            value={selectedTime}
            onChange={handleTimeChange}
            className="p-2 border rounded"
          >
            <option value="">Select Time</option>
            {getAvailableTimesForDate(selectedDate).map((time) => (
              <option key={time} value={time}>
                {time}
              </option>
            ))}
          </select>
        )}
        <Button
          variant="contained"
          disabled={!selectedDate || !selectedTime}
          onClick={() =>
            console.log(
              "Selected:",
              format(selectedDate as Date, "dd/MM/yyyy"),
              selectedTime
            )
          }
        >
          Confirm Selection
        </Button>
      </div>
    </LocalizationProvider>
  );
};

export default ScheduleDatePicker;
