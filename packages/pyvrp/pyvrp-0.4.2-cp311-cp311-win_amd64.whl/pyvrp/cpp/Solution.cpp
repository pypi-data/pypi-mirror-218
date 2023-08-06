#include "Solution.h"
#include "ProblemData.h"

#include <fstream>
#include <numeric>
#include <unordered_map>

using Client = int;
using Visits = std::vector<Client>;
using Routes = std::vector<Solution::Route>;

void Solution::evaluate(ProblemData const &data)
{
    Cost allPrizes = 0;
    for (size_t client = 1; client <= data.numClients(); ++client)
        allPrizes += data.client(client).prize;

    for (auto const &route : routes_)
    {
        // Whole solution statistics.
        numClients_ += route.size();
        prizes_ += route.prizes();
        distance_ += route.distance();
        timeWarp_ += route.timeWarp();
        excessLoad_ += route.excessLoad();
    }

    uncollectedPrizes_ = allPrizes - prizes_;
}

size_t Solution::numRoutes() const { return routes_.size(); }

size_t Solution::numClients() const { return numClients_; }

Routes const &Solution::getRoutes() const { return routes_; }

std::vector<std::pair<Client, Client>> const &Solution::getNeighbours() const
{
    return neighbours;
}

bool Solution::isFeasible() const { return !hasExcessLoad() && !hasTimeWarp(); }

bool Solution::hasExcessLoad() const { return excessLoad_ > 0; }

bool Solution::hasTimeWarp() const { return timeWarp_ > 0; }

Distance Solution::distance() const { return distance_; }

Load Solution::excessLoad() const { return excessLoad_; }

Cost Solution::prizes() const { return prizes_; }

Cost Solution::uncollectedPrizes() const { return uncollectedPrizes_; }

Duration Solution::timeWarp() const { return timeWarp_; }

void Solution::makeNeighbours()
{
    for (auto const &route : routes_)
        for (size_t idx = 0; idx != route.size(); ++idx)
            neighbours[route[idx]]
                = {idx == 0 ? 0 : route[idx - 1],                  // pred
                   idx == route.size() - 1 ? 0 : route[idx + 1]};  // succ
}

bool Solution::operator==(Solution const &other) const
{
    // First compare simple attributes, since that's quick and cheap.
    bool const simpleChecks = distance_ == other.distance_
                              && excessLoad_ == other.excessLoad_
                              && timeWarp_ == other.timeWarp_
                              && routes_.size() == other.routes_.size();

    if (!simpleChecks)
        return false;

    // Now test if the neighbours are all equal. If that's the case we have
    // the same visit structure across routes.
    if (neighbours != other.neighbours)
        return false;

    // The visits are the same for both solutions, but the vehicle assignments
    // need not be. We check this via a mapping from the first client in each
    // route to the vehicle type of that route. We need to base this on the
    // visits since the routes need not be in the same order between solutions.
    std::unordered_map<Client, VehicleType> client2vehType;
    for (auto const &route : routes_)
        client2vehType[route.visits()[0]] = route.vehicleType();

    for (auto const &route : other.routes_)
        if (client2vehType[route.visits()[0]] != route.vehicleType())
            return false;

    return true;
}

Solution::Solution(ProblemData const &data, XorShift128 &rng)
    : neighbours(data.numClients() + 1, {0, 0})
{
    // Shuffle clients (to create random routes)
    auto clients = std::vector<int>(data.numClients());
    std::iota(clients.begin(), clients.end(), 1);
    std::shuffle(clients.begin(), clients.end(), rng);

    // Distribute clients evenly over the routes: the total number of clients
    // per vehicle, with an adjustment in case the division is not perfect.
    auto const numVehicles = data.numVehicles();
    auto const numClients = data.numClients();
    auto const perVehicle = std::max<size_t>(numClients / numVehicles, 1);
    auto const perRoute = perVehicle + (numClients % numVehicles != 0);
    auto const numRoutes = (numClients + perRoute - 1) / perRoute;

    std::vector<std::vector<Client>> routes(numRoutes);
    for (size_t idx = 0; idx != numClients; ++idx)
        routes[idx / perRoute].push_back(clients[idx]);

    routes_.reserve(numRoutes);
    size_t count = 0;
    for (size_t vehType = 0; vehType != data.numVehicleTypes(); ++vehType)
    {
        auto const numAvailable = data.vehicleType(vehType).numAvailable;
        for (size_t i = 0; i != numAvailable; ++i)
            if (count < routes.size())
                routes_.emplace_back(data, routes[count++], vehType);
    }

    makeNeighbours();
    evaluate(data);
}

Solution::Solution(ProblemData const &data,
                   std::vector<std::vector<Client>> const &routes)
{
    Routes transformedRoutes;
    transformedRoutes.reserve(routes.size());
    for (auto const &visits : routes)
        transformedRoutes.emplace_back(data, visits, 0);

    *this = Solution(data, transformedRoutes);
}

Solution::Solution(ProblemData const &data, std::vector<Route> const &routes)
    : routes_(routes), neighbours(data.numClients() + 1, {0, 0})
{
    if (routes.size() > data.numVehicles())
    {
        auto const msg = "Number of routes must not exceed number of vehicles.";
        throw std::runtime_error(msg);
    }

    std::vector<size_t> visits(data.numClients() + 1, 0);
    std::vector<size_t> usedVehicles(data.numVehicleTypes(), 0);
    for (auto const &route : routes)
    {
        if (route.empty())
        {
            auto const msg = "Solution should not contain empty routes.";
            throw std::runtime_error(msg);
        }

        usedVehicles[route.vehicleType()]++;
        for (auto const client : route)
            visits[client]++;
    }

    for (size_t vehType = 0; vehType != data.numVehicleTypes(); vehType++)
        if (usedVehicles[vehType] > data.vehicleType(vehType).numAvailable)
        {
            std::ostringstream msg;
            auto const numAvailable = data.vehicleType(vehType).numAvailable;
            msg << "Used more than " << numAvailable << " vehicles of type "
                << vehType << '.';
            throw std::runtime_error(msg.str());
        }

    for (size_t client = 1; client <= data.numClients(); ++client)
    {
        if (data.client(client).required && visits[client] == 0)
        {
            std::ostringstream msg;
            msg << "Client " << client << " is required but not present.";
            throw std::runtime_error(msg.str());
        }

        if (visits[client] > 1)
        {
            std::ostringstream msg;
            msg << "Client " << client << " is visited more than once.";
            throw std::runtime_error(msg.str());
        }
    }

    makeNeighbours();
    evaluate(data);
}

Solution::Route::Route(ProblemData const &data,
                       Visits const visits,
                       size_t const vehicleType)
    : visits_(std::move(visits)), centroid_({0, 0}), vehicleType_(vehicleType)
{
    if (visits_.empty())
        return;

    for (size_t idx = 0; idx != size(); ++idx)
        release_ = std::max(release_, data.client(visits_[idx]).releaseTime);

    Duration time = std::max(release_, data.depot().twEarly);
    int prevClient = 0;

    for (size_t idx = 0; idx != size(); ++idx)
    {
        auto const &clientData = data.client(visits_[idx]);

        distance_ += data.dist(prevClient, visits_[idx]);
        duration_ += data.duration(prevClient, visits_[idx]);
        demand_ += clientData.demand;
        service_ += clientData.serviceDuration;
        prizes_ += clientData.prize;

        centroid_.first += static_cast<double>(clientData.x) / size();
        centroid_.second += static_cast<double>(clientData.y) / size();

        time += data.client(prevClient).serviceDuration
                + data.duration(prevClient, visits_[idx]);

        if (time < clientData.twEarly)  // add wait duration
        {
            wait_ += clientData.twEarly - time;
            time = clientData.twEarly;
        }

        if (time > clientData.twLate)  // add time warp
        {
            timeWarp_ += time - clientData.twLate;
            time = clientData.twLate;
        }

        prevClient = visits_[idx];
    }

    Client const last = visits_.back();  // last client has depot as successor
    distance_ += data.dist(last, 0);
    duration_ += data.duration(last, 0);

    time += data.client(last).serviceDuration + data.duration(last, 0);
    timeWarp_ += std::max<Duration>(time - data.depot().twLate, 0);

    auto const capacity = data.vehicleType(vehicleType).capacity;
    excessLoad_ = capacity < demand_ ? demand_ - capacity : 0;
}

bool Solution::Route::empty() const { return visits_.empty(); }

size_t Solution::Route::size() const { return visits_.size(); }

Client Solution::Route::operator[](size_t idx) const { return visits_[idx]; }

Visits::const_iterator Solution::Route::begin() const
{
    return visits_.cbegin();
}

Visits::const_iterator Solution::Route::end() const { return visits_.cend(); }

Visits::const_iterator Solution::Route::cbegin() const
{
    return visits_.cbegin();
}

Visits::const_iterator Solution::Route::cend() const { return visits_.cend(); }

Visits const &Solution::Route::visits() const { return visits_; }

Distance Solution::Route::distance() const { return distance_; }

Load Solution::Route::demand() const { return demand_; }

Load Solution::Route::excessLoad() const { return excessLoad_; }

Duration Solution::Route::duration() const { return duration_; }

Duration Solution::Route::serviceDuration() const { return service_; }

Duration Solution::Route::timeWarp() const { return timeWarp_; }

Duration Solution::Route::waitDuration() const { return wait_; }

Duration Solution::Route::releaseTime() const { return release_; }

Cost Solution::Route::prizes() const { return prizes_; }

std::pair<double, double> const &Solution::Route::centroid() const
{
    return centroid_;
}

size_t Solution::Route::vehicleType() const { return vehicleType_; }

bool Solution::Route::isFeasible() const
{
    return !hasExcessLoad() && !hasTimeWarp();
}

bool Solution::Route::hasExcessLoad() const { return excessLoad_ > 0; }

bool Solution::Route::hasTimeWarp() const { return timeWarp_ > 0; }

bool Solution::Route::operator==(Solution::Route const &other) const
{
    // First compare simple attributes, since that's a quick and cheap check.
    // Only when these are the same we test if the visits are all equal.

    // clang-format off
    return distance_ == other.distance_
        && demand_ == other.demand_
        && timeWarp_ == other.timeWarp_
        && vehicleType_ == other.vehicleType_
        && visits_ == other.visits_;
    // clang-format on
}

std::ostream &operator<<(std::ostream &out, Solution const &sol)
{
    auto const &routes = sol.getRoutes();

    for (size_t idx = 0; idx != routes.size(); ++idx)
        out << "Route #" << idx + 1 << ": " << routes[idx] << '\n';

    return out;
}

std::ostream &operator<<(std::ostream &out, Solution::Route const &route)
{
    for (Client const client : route)
        out << client << ' ';
    return out;
}
