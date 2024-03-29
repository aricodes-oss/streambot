package workers

import (
	"sync"

	mapset "github.com/deckarep/golang-set/v2"

	"streambot/db"
	"streambot/db/models"
)

func clean_channel(channelID string) error {
	channel, err := discordClient.Channel(channelID)
	if err != nil {
		log.Warnf("Failed to open channel %v: %v", channelID, err)
		return err
	}

	lastHundred, err := discordClient.ChannelMessages(channelID, 100, "", "", channel.LastMessageID)
	if err != nil {
		log.Warnf("Failed to fetch messages in %v: %v", channelID, err)
		return err
	}

	storedIds := []models.Stream{}
	db.Conn.Distinct("message_id").Find(&storedIds)

	knownSet := mapset.NewSet[string]()
	for _, m := range storedIds {
		knownSet.Add(m.MessageID)
	}

	toDelete := []string{}
	for _, message := range lastHundred {
		if message.Author.ID == discordClient.State.User.ID && !knownSet.Contains(message.ID) {
			toDelete = append(toDelete, message.ID)
		}
	}

	discordClient.ChannelMessagesBulkDelete(channelID, toDelete)

	return nil
}

func CleanChannelsWorker() {
	subgroup := sync.WaitGroup{}

	reservations := []models.Reservation{}
	db.Conn.Distinct("channel_id").Find(&reservations)

	for _, reservation := range reservations {
		log.Debugf("Cleaning channel ID %v", reservation.ChannelID)
		subgroup.Add(1)
		go func(cid string) {
			defer subgroup.Done()

			clean_channel(cid)
		}(reservation.ChannelID)
	}

	subgroup.Wait()
}
