
const renderChart = (data, labels) => {
  var ctx = document.getElementById("myChartCategoryExpense").getContext("2d");
  var myChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Last 6 months expenses",
          data: data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Expenses per category",
      },
    },
  });
};

const getChartData1 = () => {
  console.log("fetching");
  fetch("/expense_category_summary")
    .then((res) => res.json())
    .then((results) => {
      console.log("results", results);
      const category_data = results.expense_category_data;
      const [labels, data] = [
        Object.keys(category_data),
        Object.values(category_data),
      ];

      renderChart(data, labels);
    });
};

window.onload = getChartData1();
document.addEventListener("DOMContentLoaded", function() {
  const getChartData2 = () => {
      console.log("fetching");
      //const selectedYear=document.getElementById('selectedYear').value;
      //console.log(selectedYear);
      fetch("/expense_month_summary")
          .then((res) => res.json())
          .then((results) => {
              console.log("results", results);
              const category_data = results.expense_month_data;
              const [labels, data] = [
                  Object.keys(category_data),
                  Object.values(category_data),
              ];

              renderHistogram(data, labels,localStorage.getItem("darkMode"));
          });
  };

  const renderHistogram = (data, labels,isDarkMode) => {
      var ctx = document.getElementById("myChartMonthExpense").getContext("2d");
      var axisColor = isDarkMode ? '#ffffff' : '#000000';
      var myHistogram = new Chart(ctx, {
          type: "bar",
          data: {
              labels: labels,
              datasets: [
                {
                  label: "Monthly Expenses",
                  data: data,
                  backgroundColor: "rgba(75, 192, 192, 0.2)", 
                  borderColor: "rgba(75, 192, 192, 1)",
                  borderWidth: 2,
                },
              ],
          },
          options: {
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: 'Amount',
                  color: axisColor,
                },
                ticks: {
                  color: axisColor,
                },
              },
              x: {
                title: {
                  display: true,
                  text: 'Month',
                  color: axisColor, 
                },
                ticks: {
                  color: axisColor, 
                },
              },
            },
            responsive: true,
            maintainAspectRatio: true,
            title: {
              display: true,
              text: 'Monthly Expenses Histogram',
            },
            aspectRatio:1.5,
          },
      });
  };

  getChartData2();
});

document.addEventListener("DOMContentLoaded", function() {
  const getChartData3 = () => {
    console.log("fetching");
    fetch("/category_per_month_summary")
      .then((res) => res.json())
      .then((results) => {
        console.log("results", results);
        const category_data = results.category_month_summary;
        console.log("category_data",category_data)
        const labels = Object.keys(category_data);
        console.log("labels",labels)
        const data=Object.values(category_data)
        console.log("data",data);
        
        renderStackedChart(data, labels, localStorage.getItem("darkMode"));
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  const renderStackedChart = (data, labels, isDarkMode) => {
    // Initialize an empty array to store all categories
    let categories = [];
  
    // Loop through each month's data
    data.forEach((month) => {
      // Extract categories for the current month and add them to the categories array
      categories = categories.concat(Object.keys(month));
    });
  
    // Remove duplicate categories and keep only unique ones
    categories = Array.from(new Set(categories));
  
    // Now categories array contains all unique categories across all months
  
    const datasets = categories.map((category) => {
      return {
        label: category,
        backgroundColor: getRandomColor(), // Function to generate random color
        data: data.map((month) => month[category] || 0), // Access the category data for each month
      };
    });
  
    const ctx = document.getElementById("myChartMonthCategory").getContext("2d");
    const myChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: datasets,
      },
      options: {
        scales: {
          x: {
            stacked: true,
            title: {
              display: true,
              text: "Month",
            },
          },
          y: {
            stacked: true,
            title: {
              display: true,
              text: "Amount",
            },
          },
        },
        plugins: {
          title: {
            display: true,
            text: "Expense of category per month",
          },
        },
      },
    });
  };
  
  
  getChartData3();
});

function getRandomColor() {
  return `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.5)`;
}
